from classify import classify
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from Front_End directory
app.mount("/static", StaticFiles(directory="Front_End"), name="static")

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/app.html")

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        df = pd.read_csv(file.file)

        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'source' and 'log_message' columns"
            )

        df["target_label"] = classify(
            list(zip(df["source"], df["log_message"]))
        )

        output_file = "output.csv"
        df.to_csv(output_file, index=False)

        return FileResponse(
            output_file,
            media_type="text/csv",
            filename="output.csv"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        df = pd.read_csv(file.file)

        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'source' and 'log_message' columns"
            )

        df["target_label"] = classify(
            list(zip(df["source"], df["log_message"]))
        )

        output_file = "output.csv"
        df.to_csv(output_file, index=False)

        return FileResponse(
            output_file,
            media_type="text/csv",
            filename="output.csv"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()
