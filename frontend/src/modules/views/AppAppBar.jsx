import * as React from 'react';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import ArrowBackIcon from '@mui/icons-material/ArrowBack'; // 导入返回图标
import IconButton from '@mui/material/IconButton';
import AppBar from '../components/AppBar';
import Toolbar from '../components/Toolbar';
import { Link as RouterLink, useLocation, useNavigate } from 'react-router-dom';

const rightLink = {
  fontSize: 16,
  color: 'common.white',
  ml: 3,
};

function AppAppBar() {
  const location = useLocation();
  const navigate = useNavigate();
  // 确保返回按钮仅在有历史记录时显示
  const canGoBack = location.pathname !== '/'; // 可以根据需要调整条件
  
  // Determine the link text and href based on the current path
  let linkText = 'Add Movie';
  let linkHref = '/AddMovie';
  if (location.pathname === '/AddMovie') {
    linkText = 'Home';
    linkHref = '/';
  }

  return (
    <div>
      <AppBar position="fixed">
        <Toolbar sx={{ justifyContent: 'space-between' }}>

          {canGoBack && (
            <IconButton
              edge="start"
              color="inherit"
              aria-label="back"
              onClick={() => navigate(-1)} // 返回上一页
              sx={{ mr: 2 }}
            >
              <ArrowBackIcon />
            </IconButton>
          )}

          <Box sx={{ flex: 1 }} />
          <Link
            component={RouterLink}
            to={linkHref}
            variant="h6"
            underline="none"
            color="inherit"
            sx={{ fontSize: 24 }}
          >
            {linkText}
          </Link>
          <Box sx={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
            <Link
              color="inherit"
              variant="h6"
              underline="none"
              href="/SignIn"
              sx={rightLink}
            >
              {'Sign In'}
            </Link>
            <Link
              variant="h6"
              underline="none"
              href="/MovieDetail"
              sx={{ ...rightLink, color: 'secondary.main' }}
            >
              {'Sign Up'}
            </Link>
          </Box>
        </Toolbar>
      </AppBar>
      <Toolbar />
    </div>
  );
}

export default AppAppBar;
