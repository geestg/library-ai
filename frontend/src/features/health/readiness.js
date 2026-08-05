import { backendService } from "../backend/service";
export class ReadinessService {
    async check() {
        try {
            await backendService.health.check();
            return {
                healthy: true,
            };
        }
        catch {
            return {
                healthy: false,
            };
        }
    }
}
export const readinessService = new ReadinessService();
