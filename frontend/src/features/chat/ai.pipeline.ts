import type {
    ChatRequest,
    RetrievalResponse,
} from "../../contracts";

import {
    hybridRetrievalService,
} from "../retrieval/hybrid";

export interface AIResponse {

    answer: string;

    retrieval: RetrievalResponse;

}

export class AIResponsePipeline {

    async execute(
        request: ChatRequest,
    ): Promise<AIResponse> {

        const retrieval =
            await hybridRetrievalService.search({

                query: request.message,

                workspaceId:
                    request.workspaceId,

                topK: 8,

            });

        return {

            answer: "",

            retrieval,

        };

    }

}

export const aiPipeline =
    new AIResponsePipeline();
