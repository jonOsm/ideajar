import { ValidationRules } from './validation'

export const ErrorCodes = {
    LOGIN_BAD_CREDENTIALS: 'LOGIN_BAD_CREDENTIALS',
    REGISTER_USER_ALREADY_EXISTS: 'REGISTER_USER_ALREADY_EXISTS',
    REGISTER_INVALID_PASSWORD: 'REGISTER_INVALID_PASSWORD',
    REGISTER_INVALID_USERNAME_LENGTH: 'REGISTER_INVALID_USERNAME_LENGTH',
    REGISTER_INVALID_USERNAME_FORMAT: 'REGISTER_INVALID_USERNAME_FORMAT',
} as const

export const ErrorMessages = {
    [ErrorCodes.LOGIN_BAD_CREDENTIALS]: 'Incorrect email or password.',
    [ErrorCodes.REGISTER_USER_ALREADY_EXISTS]: 'A user with this email or username already exists.',
    [ErrorCodes.REGISTER_INVALID_PASSWORD]: `Password must be at least ${ValidationRules.MIN_PASSWORD_LENGTH} characters long.`,
    [ErrorCodes.REGISTER_INVALID_USERNAME_LENGTH]: `Username must be between ${ValidationRules.USERNAME_MIN_LENGTH} and ${ValidationRules.USERNAME_MAX_LENGTH} characters.`,
    [ErrorCodes.REGISTER_INVALID_USERNAME_FORMAT]: 'Username can only contain letters, numbers, and underscores.',
    DEFAULT_LOGIN: 'Login failed. Please check your credentials.',
    DEFAULT_REGISTER: 'Registration failed. Please try again.',
    DEFAULT_UNKNOWN: 'An unexpected error occurred.',
} as const

export const getReadableError = (error: any, defaultMsg: string = ErrorMessages.DEFAULT_UNKNOWN): string => {
    if (error?.body?.detail) {
        const detail = error.body.detail

        // Check if detail matches a known error code
        if (detail in ErrorMessages) {
            return ErrorMessages[detail as keyof typeof ErrorMessages]
        }

        // Fallback if detail is just a raw string message
        if (typeof detail === 'string') {
            return detail
        }
    }
    return defaultMsg
}
