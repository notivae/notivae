import mitt from "mitt";
import type { WebSocketOutgoingEvents } from "@/types/ws.ts";
import { WSStatusCode } from "@/lib/wsStatusCodes.ts";


const WS_URL = '/api/ws';


type BusEvents = {
    open: void
    close: void
    error: Event
    message: { type: string, payload: string }
    raw: MessageEvent
}


export const socketBus = mitt<BusEvents>();


let ws: WebSocket | null = null;
let reconnectAttempts: number = 0;
let isConnected: boolean = false;


function connectWebSocket(): void {
    if (isConnected) return;
    console.info("[WS] Connecting web socket...");

    ws = new WebSocket(WS_URL);
    isConnected = true;

    ws.addEventListener('open', () => {
        console.info('[WS] WebSocket connected');
        socketBus.emit('open');
        reconnectAttempts = 0;
    });

    ws.addEventListener('message', (event) => {
        socketBus.emit('raw', event);
        try {
            const data = JSON.parse(event.data);
            socketBus.emit('message', data);
        } catch (e) {
            console.error('[WS] Invalid WS Message', event.data);
        }
    });

    ws.addEventListener('close', (event) => {
        console.info(`[WS] WebSocket disconnected (${event.code}: ${event.reason})`);
        isConnected = false;
        socketBus.emit('close');
        if (event.code === WSStatusCode.WS_1008_POLICY_VIOLATION) {
            reconnectAttempts += 2;
        }
        scheduleReconnect();
    });

    ws.addEventListener('error', (e) => {
        console.error('[WS] WebSocket error', e);
        socketBus.emit('error', e);
    });
}


function scheduleReconnect(): void {
    const delay = Math.min(30_000, 1000 * Math.pow(2, reconnectAttempts));
    console.info(`[WS] Reconnecting in ${delay.toFixed(0)}ms`);
    setTimeout(() => {
        reconnectAttempts++;
        connectWebSocket();
    }, delay);
}



export function sendMessage<K extends keyof WebSocketOutgoingEvents>(type: K, payload: WebSocketOutgoingEvents[K]): void {
    const msg = { type, payload };
    if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(msg));
    }
}


connectWebSocket();
