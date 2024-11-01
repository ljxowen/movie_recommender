import { UserMovieService } from "../client/services";

export const addLikedMovie = async (id) => {
    try {
        const response = await UserMovieService.addUserMovie({ id })
        return response 
    } catch (err) {
        throw err;
    }
}

export const removeLikedMovie = async (id) => {
    try {
        const response = await UserMovieService.removeUserMovie({ id })
        return response 
    } catch (err) {
        throw err;
    }
}

export const readLikedMovie = async () => {
    try {
        const response = await UserMovieService.readUserMovie()
        return response 
    } catch (err) {
        throw err;
    }
}