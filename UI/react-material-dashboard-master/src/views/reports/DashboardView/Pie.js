import React, { Component, useState } from 'react';
import {
  Box,
  Container
} from '@material-ui/core';
import Page from 'src/components/Page';
import victory from "victory";
import {
  VictoryPie
} from "victory";


class Pie extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sets: [],
      data: [],
      testData: []
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
          <Box mt={1}>
            <div
              spacing={3}
              style={{height: 400}}
            >
              <VictoryPie
                data={this.state.sets}
                style={{
                  data: { fill: (d) => d.datum.color } 
                }}
              />
            </div>
          </Box>
        </Container>
      </Page>
  
    )
  }

}

export default Pie;
