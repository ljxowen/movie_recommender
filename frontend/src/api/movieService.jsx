import { MoviesService } from "../client/services";


export const fetchMovies = async () => {
    try {
        const response = await MoviesService.readMovies();
        return response; 
    } catch (err) {
        // console.error('Error fetching movies:', err);
        throw err; // 将错误重新抛出，以便在调用处捕获
    } 
};

export const fetchMovie = async (id) => {
    try {
        const response = await MoviesService.readMovie( { id } );
        return response;
    } catch (err) {
        throw err;
    }
}

export const fetchLikedMovie = async () => {
    try {
        const response = await MoviesService.readLikedMovies();
        return response;
    } catch (err) {
        throw err;
    }
}
