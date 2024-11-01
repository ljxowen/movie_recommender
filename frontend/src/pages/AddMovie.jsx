import * as React from 'react';
import AppAppBar from '../modules/views/AppAppBar';
import withRoot from '../modules/withRoot';
import AddMovieSection from '../modules/views/AddMovieSection'

function AddMovie() {
  return (
    <React.Fragment>
      <AppAppBar />
      <AddMovieSection />
    </React.Fragment>
  );
}

export default withRoot(AddMovie);