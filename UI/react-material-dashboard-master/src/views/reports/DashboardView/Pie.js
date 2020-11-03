import React, { Component, useState } from 'react';
import {
  Box,
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import Paper from '@material-ui/core/Paper';
import {
  Chart,
  PieSeries,
  Title,
} from '@devexpress/dx-react-chart-material-ui';
import { Animation } from '@devexpress/dx-react-chart';


class Pie extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sets: [],
      data: []
    };
  }

  componentDidMount(){
    fetch("http://127.0.0.1:5000/collection/array?company=nike&set=arnav")
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
    console.log(this.state.sets)
    const { data: chartData } = this.state.data;
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
