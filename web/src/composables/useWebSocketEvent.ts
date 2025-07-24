import type { WebSocketIncomingEvents } from "@/types/ws.ts";
import { onBeforeUnmount, onMounted } from "vue";
import { socketBus } from "@/services/ws";


export function useWebSocketEvent<K extends keyof WebSocketIncomingEvents>(
    type: K,
    handler: (payload: WebSocketIncomingEvents[K]) => void
) {
    function internalHandler(e: { type: string, payload: unknown }) {
        if (e.type === type) {
            handler(e.payload as WebSocketIncomingEvents[K]);
        }
    }

    onMounted(() => socketBus.on('message', internalHandler));
    onBeforeUnmount(() => socketBus.off('message', internalHandler));
}
