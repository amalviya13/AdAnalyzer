import React from 'react';
import {
  Box,
  Container
} from '@material-ui/core';
import Page from 'src/components/Page';
import {
    VictoryChart,
    VictoryBar
  } from "victory";


class Top5Bar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sets: [],
      data: [],
      testData: []
    };
  }

  componentDidMount(){
    var url = "http://127.0.0.1:5000/set/top5/best?set=" + this.props["setName"] + "&company=" + this.props["company"]
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
                <VictoryChart domainPadding={40}>
                    <VictoryBar
                        horizontal
                        style={{ data: { fill: '#F1737F' }}}
                        events={[{
                            target: "data",
                            eventHandlers: {
                              onClick: () => {
                                return [
                                  {
                                    target: "data",
                                    mutation: (props) => {
                                      const fill = props.style && props.style.fill;
                                      return fill === "black" ? null : { style: { fill: "black" } };
                                    }
                                  }
                                ];
                              }
                            }
                        }]}
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

export default Top5Bar;
