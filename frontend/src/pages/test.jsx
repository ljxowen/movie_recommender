import * as React from 'react';
import AppAppBar from '../modules/views/AppAppBar';
import withRoot from '../modules/withRoot';
import MovieDetail from './MovieDetail';

function MovieDetail() {
  return (
    <React.Fragment>
      <AppAppBar />
      <MovieDetail />
    </React.Fragment>
  );
}

export default withRoot(MovieDetail);