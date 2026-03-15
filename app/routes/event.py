from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi import FastAPI, UploadFile, File
from database.database import get_session
from models.event import Event, EventCreate 
from models.model import Model
from services.crud import event as EventService
from typing import List
import logging
import shutil
import os
import json
from services.rm import rm as rm_module


# Configure logging
logger = logging.getLogger(__name__)

event_router = APIRouter()


UPLOAD_DIR = "../data/images" 
os.makedirs(UPLOAD_DIR, exist_ok=True)

@event_router.get(
    "/", 
    response_model=List[Event],
    summary = "Get all events",
    response_description="List of all events") 
async def get_all_events(session=Depends(get_session)) -> List[Event]:
    """
    Get list of all events.

    Args:
        session: Database session

    Returns:
        List[TransactionResponse]: List of events
    """
    try:
        events = EventService.get_all_events(session)
        logger.info(f"Retrieved {len(events)} events")
        return events
    except Exception as e:
        logger.info(f"Error retrieving events: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving events"
        )    


@event_router.get("/{id}", response_model=Event) 
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    try:
        event = EventService.get_event_by_id(id, session)
    except Exception as e:
        logger.error(f"Database error: {str(e)}")   
    if event is None:
        logger.warning(f"Event with id {id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Event with supplied ID does not exist"
        )

    logger.info(f"Retrieved event {id}")
    return event


"""
    @event_router.post("/new")
    async def create_event( creator_id: int, model : Model = Depends(get_model),
                            event_data: EventCreate = Body(...),
                            session=Depends(get_session)) -> dict: 
        try:
            EventService.create_event(
            event_data = event_data, 
            creator_id = creator_id,
            model = model,
            session = session)
            return {"message": "Event created successfully"}
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error {type(e).__name__}: {str(e)}")
"""


@event_router.post("/upload_image/")
async def upload_image(creator_id: int, file: UploadFile = File(...),
                        session=Depends(get_session)
                        ):
    if not file.filename.lower().endswith(("png", "jpg", "jpeg")):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        new_event = EventService.create_event(
                image = file_path, 
                creator_id = creator_id,
                session = session)

        task_worker = {
            "event_id": new_event.id,  
            "image_path": file_path
        }
        rm_module.send_task(json.dumps(task_worker))
                   
        return {"message": f"File {file.filename} uploaded", "event_id" : new_event.id}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Internal Server Error {type(e).__name__}: {str(e)}")


@event_router.get("/prediction/{id}") 
async def retrieve_prediction(id: int, session=Depends(get_session)):
    try:
        prediction = EventService.get_prediction_by_id(id, session)
    except Exception as e:
        logger.error(f"Database error: {str(e)}")   
    if prediction is None:
        logger.warning(f"Event with id {id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Event with supplied ID does not exist"
        )

    logger.info(f"Retrieved prediction for event {id}")
    return {"event_id": id, "prediction": prediction}

'''
@event_router.delete("/{id}")
async def delete_event(id: int) -> dict: 
    for event in events:
        if event.id == id: 
            events.remove(event)
            return {"message": "Event deleted successfully"}
        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, detail="Event with supplied ID does not exist")

@event_router.delete("/")
async def delete_all_events() -> dict: 
    events.clear()
    return {"message": "Events deleted successfully"}
    '''