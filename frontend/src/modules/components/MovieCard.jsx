import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';

import { useNavigate } from 'react-router-dom';

export default function MovieCard({ id, title, imageUrl, rating }) {
  const navigate = useNavigate(); // 将 useNavigate 调用移到组件的顶层

  const handleClick = () => {
    navigate(`/MovieDetail/${id}`);
  };

    return (
        <Card
        sx={{
          width: 200,
          height: 400,
          margin: 2,
          cursor: 'pointer',
          transition: 'transform 0.3s ease-in-out', // 设置动画过渡效果
          '&:hover': {
            transform: 'scale(1.05)', // 鼠标悬停时放大
            boxShadow: 6, // 添加阴影效果
          },
        }}
        onClick={ handleClick }
      >
        <CardMedia
          component="img"
          height="320"
          image={imageUrl}
          alt={title}
        />
        <CardContent sx={{ height: 80, overflow: 'hidden', textOverflow: 'ellipsis' }}>
          <Typography gutterBottom variant="body1" component="div" align="center" noWrap>
            {title}
          </Typography>
          <Typography variant="body2" color="text.secondary" align="center">
            {rating}
          </Typography>
        </CardContent>
      </Card>
    );
  }


