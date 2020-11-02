import React, { Component, useState } from 'react';
import {
  Box,
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import { Pagination } from '@material-ui/lab';
import Page from 'src/components/Page';

class Pie extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sets: []
    };
  }

  componentDidMount(){
    fetch("http://127.0.0.1:5000/collection/array?company=nike&set=arnav")
      .then(res => res.json())
      .then(
        (result) => {
          console.log(result)
          this.setState({
            sets: result[0]
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
          <Box mt={3}>
            <Grid
              container
              spacing={3}
            >
            </Grid>
          </Box>
        </Container>
      </Page>
    )
  }

}

export default Pie;
