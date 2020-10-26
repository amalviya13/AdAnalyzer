import React, { Component, useState } from 'react';
import {
  Box,
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import { Pagination } from '@material-ui/lab';
import Page from 'src/components/Page';
import Toolbar from './Toolbar';
import ProductCard from './ProductCard';
import data from './data';

class ProductList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sets: []
    };
  }

  componentDidMount(){
    fetch("http://127.0.0.1:5000/collections?company=nike")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            sets: result
          });
        },
        (error) => {
          this.setState({
            sets: []
          });
        }
      )
  }

  render() {
    return (
      <Page title="Sets">
        <Container maxWidth={false}>
          <Toolbar />
          <Box mt={3}>
            <Grid
              container
              spacing={3}
            >
              {this.state.sets.map((set) => (
                <Grid
                  item
                  key={set}
                  lg={4}
                  md={6}
                  xs={12}
                >
                  <ProductCard
                    className={set}
                    product={set}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        </Container>
      </Page>
    )
  }

// const useStyles = makeStyles((theme) => ({
//   root: {
//     backgroundColor: theme.palette.background.dark,
//     minHeight: '100%',
//     paddingBottom: theme.spacing(3),
//     paddingTop: theme.spacing(3)
//   },
//   productCard: {
//     height: '100%'
//   }
// }));

//   const classes = useStyles();
//   const [products] = useState(data);

//   return (
//     <Page
//       className={classes.root}
//       title="Products"
//     >
      // <Container maxWidth={false}>
      //   <Toolbar />
      //   <Box mt={3}>
      //     <Grid
      //       container
      //       spacing={3}
      //     >
      //       {products.map((product) => (
      //         <Grid
      //           item
      //           key={product.id}
      //           lg={4}
      //           md={6}
      //           xs={12}
      //         >
      //           <ProductCard
      //             className={classes.productCard}
      //             product={product}
      //           />
      //         </Grid>
      //       ))}
      //     </Grid>
      //   </Box>
      //   <Box
      //     mt={3}
      //     display="flex"
      //     justifyContent="center"
      //   >
      //     <Pagination
      //       color="primary"
      //       count={3}
      //       size="small"
      //     />
      //   </Box>
      // </Container>
//     </Page>
//   );

}

export default ProductList;