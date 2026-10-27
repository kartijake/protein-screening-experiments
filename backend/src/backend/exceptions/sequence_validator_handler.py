from fastapi import Request
from backend.services.sequence_validator import SequenceValidationError
from fastapi.responses import JSONResponse
import logging
logger = logging.getLogger(__name__)

def sequence_validator(request:Request,exc:SequenceValidationError):
       
       logger.error(
            "Amino acid Sequence Error | %s %s | RID:%s",
            request.method,
            request.url.path,
            getattr(request.state, "request_id", "unknown"),
            exc_info=str(exc),
    )
        
       return JSONResponse(
               status_code=422,
               content={
                    "error": "Amino acid sequence validation failed",
                    "details": str(exc),
               }
              
           )
