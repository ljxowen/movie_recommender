import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import MovieCard from '../components/MovieCard'; 

import { fetchLikedMovie } from '../../api/movieService'
import { OpenAPI } from '../../client/core/OpenAPI';
import {getToken} from '../../utils/loginToken'

 const MyMovieSection = () => {
    const [movies, setMovies] = useState([]); // state for movie data

    useEffect(() => {

        OpenAPI.TOKEN = getToken();

        const fetchData = async () => {
            try {
                // 获取电影数据
                const moviesResponse = await fetchLikedMovie();
                setMovies(moviesResponse.data); // 根据实际 API 数据结构调整
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData()
    }, []); //只在组件挂在时执行

    return (
        <Container maxWidth="xl" component="section" sx={{ mt: 8, mb: 4 }}>
            <Typography variant="h4" marked="center" align="center" component="h2"> 
                The Movie You Like
            </Typography>
            <Box
                sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    justifyContent: 'flex-start',
                    alignItems: 'center',
                    p: 2,
                }}
            >
                {movies.map((movie) => (
                    <MovieCard
                    key={movie.id}
                    id={movie.id}
                    title={movie.title}
                    imageUrl={movie.poster}
                    rating={movie.imdb_rating}
                    // onClick={() => alert(`${movie.title} clicked!`)} // 处理点击事件
                    />
                ))}
            </Box>
        </Container>
      );

 }

 export default MyMovieSection;