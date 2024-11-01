import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Container from '@mui/material/Container';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import Button from '../modules/components/Button';
import { fetchMovie } from '../api/movieService';
import { addLikedMovie, removeLikedMovie, readLikedMovie } from '../api/userMovieService';
import { OpenAPI } from '../client/core/OpenAPI';
import {getToken} from '../utils/loginToken'
import AppAppBar from '../modules/views/AppAppBar';
import withRoot from '../modules/withRoot';

function MovieDetail( ) {
  // 获取传递的参数，这里假设通过URL传递电影的ID
  let { id } = useParams();
  const [movie, setMovie] = useState({}); // state for movie data
  const [isliked, setLike] = useState(false); // state for Like/Dislike

  id = parseInt(id, 10); //将字符转换为int

  // 读取电影数据api
  useEffect(() => {
    OpenAPI.TOKEN = getToken();

    // 读取电影详情
    fetchMovie(id) 
      .then((response) => {
        setMovie(response);
      }).catch((error) => {
        console.error('Error fetching movie', error);
      });

    //读取liked电影ids
    readLikedMovie()
      .then((response) => {
        if (response.movies.includes(id)) {
          setLike(true); //如果当前电影id已存在用户喜爱列表，设置为true
        }
      }).catch((err) => {
        console.error("Error fetching user liked movie id", err);
      });

  }, [id]); //// 依赖于 id，当id改变时重新执行

  // Handle Like/Dislike button 
  const handleLikeButton = () => {
    if (isliked) {
      // if is liked(true), call remove api
      removeLikedMovie(id)
        .then((response) => {
          setLike(false);
          console.log(response); // return have no actual use here
        }).catch((error) => {
          console.error("Error remove user movie id", error);
        });
    } else {
      // if is not liked(false), call add api
      addLikedMovie(id)
        .then((response) => {
          setLike(true);
          console.log(response); // return have no actual use here
        }).catch((error) => {
          console.error("Error add user movie id", error);
        });
    }
  };

  return (
    <React.Fragment>
      <AppAppBar />

      <Container component="main" sx={{ mt: 8, mb: 4 }}>
        <Card sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, padding: 2 }}>
          <CardMedia
            component="img"
            sx={{ width: { xs: '100%', md: 400 }, height: { xs: 'auto', md: 600 }, marginRight: 2 }}
            image={movie.poster}
            alt={movie.title}
          />
          <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flex: '1 0 auto' }}>
              <Typography component="h2" variant="h4" gutterBottom>
                {movie.title}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                Genre: {movie.genre}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                Rating: {movie.imdb_rating}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                Release Date: {movie.released}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                Director: {movie.director}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                Cast: {movie.actors}
              </Typography>
              <Typography variant="body1" paragraph sx={{ mt: 4 }}>
                {movie.plot}
              </Typography>
            </CardContent>

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Button
                color="secondary"
                size="large"
                variant="contained"
                sx={{ mr: 2 , backgroundColor: 'red'}}
                onClick = {handleLikeButton}
              >
                  {isliked ? 'DISALIKE' : 'LIKE'}
              </Button>
            </Box>

          </Box>
        </Card>
      </Container>

    </React.Fragment>
  );
}

export default withRoot(MovieDetail);


