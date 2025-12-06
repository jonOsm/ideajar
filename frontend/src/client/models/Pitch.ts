/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Pitch = {
    id: string;
    title: string;
    description: string;
    type: Pitch.type;
    submitter?: string;
};
export namespace Pitch {
    export enum type {
        IDEA = 'idea',
        OPINION = 'opinion',
        PITCH = 'pitch',
    }
}

