import React from 'react';
import {
  Box,
  Container
} from '@material-ui/core';
import Page from 'src/components/Page';
import {
    VictoryChart,
    VictoryHistogram
  } from "victory";


class Histogram extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sets: [],
      data: [],
      testData: []
    };
  }

  componentDidMount(){
    var url = "http://127.0.0.1:5000/image/set/CTR?company=" + this.props["company"] + "&set=" + this.props["setName"]
    fetch(url)
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
          <Box mt={1}>
            <div
              spacing={3}
              style={{height: 400}}
            >
                <VictoryChart>
                    <VictoryHistogram
                        style={{ data: { fill: '#F1737F' }}}
                        animate={{
                            duration: 2000,
                            onLoad: { duration: 1000 }
                        }}
                        bins={[0, .05 , .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .85, .9, .95, 1]}
                        cornerRadius={3}
                        data={this.state.sets}
                    />
                </VictoryChart>
            </div>
          </Box>
        </Container>
      </Page>
  
    )
  }

}

export default Histogram;
