/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Vote = {
    pitch_id: string;
    vote_type: Vote.vote_type;
};
export namespace Vote {
    export enum vote_type {
        LIKE = 'like',
        DISLIKE = 'dislike',
    }
}

