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
import SetCard from './SetCard';
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
          console.log(result)
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
    console.log(this.state.sets)
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
                  <SetCard
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

}

export default ProductList;
