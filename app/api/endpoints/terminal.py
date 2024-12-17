from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from api.dependencies import get_terminal_manager

router = APIRouter()

@router.websocket("/ws/terminal/")
async def terminal_websocket(
    websocket: WebSocket,
    terminal=Depends(get_terminal_manager)
):
    await websocket.accept()
    
    await websocket.send_json({
        'response': "Connected to the terminal. Type 'help' for a list of commands.",
        'current_dir': terminal.get_relative_path_display()
    })

    try:
        while True:
            data = await websocket.receive_json()
            command = data.get('command', '')
            response = await terminal.process_command(command)
            await websocket.send_json({
                'response': response,
                'current_dir': terminal.get_relative_path_display()
            })
    except WebSocketDisconnect:
        pass
