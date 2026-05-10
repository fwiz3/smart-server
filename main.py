from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Smart Server is running"}

app.include_router(
    router=__import__("v1.routes.addDevices.add_devices", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Add Device"],
)

app.include_router(
    router=__import__("v1.routes.device.get_device", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Get device"],
)
app.include_router(
    router=__import__("v1.routes.getDevices.get_all_devices", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Get all devices"],
)
app.include_router(
    router=__import__("v1.routes.update.update_device", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Update device"],
)
app.include_router(
    router=__import__("v1.routes.removeDevice.remove_devices", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Remove devices"],
)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
