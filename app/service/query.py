
from ..db.database import db
from bson import ObjectId
from fastapi import HTTPException


async def query_thread(practice_id: int, doctor_id: int ):
    try:
        # Convert string parameters to integers
        practice_id_int = int(practice_id)
        doctor_id_int = int(doctor_id)
        
        # Query the database
        thread = await db.get_collection('lantum_message_threads').find_one({
            "practice_id": practice_id_int,
            "doctor_id": doctor_id_int
        })

        # Check if thread exists
        if thread is None:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        # Convert ObjectId to string for JSON serialization
        thread['_id'] = str(thread['_id'])
        
        return thread
    except HTTPException:
        # Re-raise HTTPExceptions (like 404) as-is
        raise
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid practice_id or doctor_id - must be numbers")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying thread: {e}")




async def query_message(practice_id: int, doctor_id: int):

    thread = await query_thread(practice_id, doctor_id)

    try:
        # Convert to integers
        doctor_id_int = int(doctor_id)
        
        messages = await db.get_collection('lantum_messages').find({ 
            "thread_id": thread['id']
        }).to_list(length=None)

        # Count sent vs received while filtering
        sent_count = 0
        received_count = 0
        
        # Return only specific fields from each message
        filtered_messages = []
        for message in messages:
            user_id = message.get('user_id')
            
            # Count messages
            if user_id == doctor_id_int:
                sent_count += 1  # Doctor sent this
            else:
                received_count += 1  # Reply from practice
            
            # Add to filtered messages
            filtered_messages.append({
                "_id": str(message['_id']),
                "body": message.get('body'),
                "user_id": message.get('user_id'),
                "doctor_id": message.get('doctor_id'),
                "is_read": message.get('is_read')
            })
        
        # Return messages + summary
        return {
            "summary": {
                "messages_sent": sent_count,
                "messages_received": received_count,
                "total_messages": sent_count + received_count
            },
            "messages": filtered_messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying messages: {e}")

async def get_doctor_info(doctor_id: int):

    doctor = await db.get_collection('booking_users').find_one({ "id": int(doctor_id) })
    if doctor is None:
        raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} not found in booking_users collection")
    
    doctor['_id'] = str(doctor['_id'])

    response = {
        "display_name": doctor['display_name'],
    }

    return response

async def get_practice_detail(practice_id: int):

    practice = await db.get_collection('booking_practices').find_one({ "id": int(practice_id) })
    if practice is None:
        raise HTTPException(status_code=404, detail=f"Practice with id {practice_id} not found in booking_practices collection")
    
    practice['_id'] = str(practice['_id'])

    response = {
        "name": practice['name'],
    }

    return response