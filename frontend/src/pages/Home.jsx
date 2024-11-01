import * as React from 'react';
import ProductCategories from '../modules/views/ProductCategories';
import ProductHowItWorks from '../modules/views/ProductHowItWorks';
import AppAppBar from '../modules/views/AppAppBar';
import withRoot from '../modules/withRoot';
import MyMovieSection from '../modules/views/MyMovieSection'

function Index() {
  return (
    <React.Fragment>
      <AppAppBar />
      <MyMovieSection />
      {/* <ProductCategories />
      <ProductHowItWorks /> */}
    </React.Fragment>
  );
}

export default withRoot(Index);