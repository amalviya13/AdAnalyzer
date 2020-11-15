import React, { Component, useState } from 'react';
import {
  Box,
  Container
} from '@material-ui/core';
import Page from 'src/components/Page';
import { ResponsiveBar } from '@nivo/bar'


class Bar extends React.Component {
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
    this.state.testData =   [
        {
          "country": "AD",
          "hot dog": 98,
          "hot dogColor": "hsl(189, 70%, 50%)",
        },
        {
        "country": "AE",
        "hot dog": 51,
        "hot dogColor": "hsl(242, 70%, 50%)",
        },
        {
        "country": "AF",
        "hot dog": 98,
        "hot dogColor": "hsl(220, 70%, 50%)",
        },
        {
        "country": "AG",
        "hot dog": 186,
        "hot dogColor": "hsl(187, 70%, 50%)",
        },
        {
        "country": "AI",
        "hot dog": 184,
        "hot dogColor": "hsl(209, 70%, 50%)",
        },
        {
        "country": "AL",
        "hot dog": 93,
        "hot dogColor": "hsl(257, 70%, 50%)",
        },
        {
        "country": "AM",
        "hot dog": 61,
        "hot dogColor": "hsl(54, 70%, 50%)",
        }
        ]

    const { data: chartData } = this.state.data;
    return (

      <Page title="Sets">
        <Container maxWidth={false}>
          <Box mt={1}>
            <div
              spacing={3}
              style={{height: 400}}
            >
              <ResponsiveBar
                data={this.state.testData}
                keys={[ 'hot dog']}
                indexBy="country"
                margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
                padding={0.3}
                valueScale={{ type: 'linear' }}
                colors={{ scheme: 'nivo' }}
                borderColor={{ from: 'color', modifiers: [ [ 'darker', 1.6 ] ] }}
                axisTop={null}
                axisRight={null}
                axisBottom={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Set Name',
                    legendPosition: 'middle',
                    legendOffset: 32
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'CTR',
                    legendPosition: 'middle',
                    legendOffset: -40
                }}
                labelSkipWidth={12}
                labelSkipHeight={12}
                labelTextColor={{ from: 'color', modifiers: [ [ 'darker', 1.6 ] ] }}
                animate={true}
                motionStiffness={90}
                motionDamping={15}
            />
            </div>
          </Box>
        </Container>
      </Page>
  
    )
  }

}

export default Bar;
