/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Pitch } from '../models/Pitch';
import type { Vote } from '../models/Vote';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PitchesService {
    /**
     * Get Pitches
     * Get a list of pitches to swipe on.
     * @returns Pitch Successful Response
     * @throws ApiError
     */
    public static getPitches(): CancelablePromise<Array<Pitch>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/pitches',
        });
    }
    /**
     * Submit Vote
     * Submit a swipe vote.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static submitVote(
        requestBody: Vote,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/vote',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
