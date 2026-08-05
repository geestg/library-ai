import { backendService } from "../backend/service";

export interface ReadinessState {
    healthy: boolean;
}

export class ReadinessService {

    async check(): Promise<ReadinessState> {

        try {

            await backendService.health.check();

            return {
                healthy: true,
            };

        } catch {

            return {
                healthy: false,
            };

        }

    }

}

export const readinessService =
    new ReadinessService();
