from fastapi import FastAPI

app = FastAPI()
app.include_router(
    router=__import__("v1.routes.addDevices.controller.add_devices", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Add Device"],
)
# app.include_router(
#     router=__import__("v1.routers.toggle_state", fromlist=["router"]).router,
#     prefix="/api/v1",
#     tags=["Toggle Device State"],
# )
app.include_router(
    router=__import__("v1.routes.device.controllers.get_device", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Get device"],
)
app.include_router(
    router=__import__("v1.routes.getDevices.controller.get_all_devices", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Get all devices"],
)
app.include_router(
    router=__import__("v1.routes.removeDevice.controller.remove_devices", fromlist=["router"]).router,
    prefix="/api/v1",
    tags=["Remove devices"],
)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)