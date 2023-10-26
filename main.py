from fastapi import FastAPI
from functions import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    root_path='/',
    title="AntiScam API",
    description="API for AntiScam",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/antiscam.json",
    summary="API created by Diyarbek Oralbaev. This api is used for AntiScam project. This project is created for the purpose of preventing phishing attacks. This project is open source.",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"Project": "AntiScam API"}


@app.post("/add_scam")  # Request to scam site
async def add_scam(site: Site):
    await add_sites(site)
    return {"message": "Success"}, 200


@app.get("/get_scam")  # Get all scam sites
async def get_scam():
    scam = await get_scam_sites()
    json ={}
    for i in scam:
        json[i[0]] = {
            "url": i[1],
            "category": i[2],
        }
    return json

@app.post("/verify_scam")  # Verify scam site
async def verify_scam(id: int):
    verify = await verify_site(id)
    return {"message": "Success"}


@app.get("/get_unverified")  # Get all unverified scam sites
async def get_unverified():
    unvscam = await get_unverified_sites()
    json ={}
    for i in unvscam:
        json[i[0]] = {
            "url": i[1],
            "category": i[2],
        }


@app.post("/delete_scam")  # Delete scam site
async def delete_scam(id: int):
    await delete_site(id)
    return {"message": "Success"}


@app.post("/check")
async def check(url: str):
    if not url.startswith("http") or not url.startswith("https"):
        return {"error": "Invalid URL"}, 400
    else:
        result = await check_url(url)
        return result