import React from 'react';
import {
  Box,
  Container
} from '@material-ui/core';
import Page from 'src/components/Page';
import {
  VictoryPie
} from "victory";


class Pie extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sets: [
        {x: '', y: 0},
        {x: '', y: 1},
        {x: '', y: 2},
        {x: '', y: 3},
        {x: '', y: 4},
        {x: '', y: 5},
        {x: '', y: 6},
        {x: '', y: 7}
      ],
      data: [],
      testData: []
    };
  }

  componentDidMount(){
    fetch("http://127.0.0.1:5000/image/array?company=nike&set=arnav&imageName=/Users/arnavmalviya/Desktop/COD/693767_1214699_bundle_archive/doom/3orpc5p97to41.jpg")
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
              <VictoryPie
                data={this.state.sets}
                innerRadius = {15}
                padAngle={5}
                radius = {125}
                labels={() => null}
                animate={{ duration: 2000 }}
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
