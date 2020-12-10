import React from 'react';
import {
  Box,
  Container,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import Results from './Results';
import Toolbar from './Toolbar';
/*
const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

const classes = useStyles();
const [customers] = useState(data);*/

class SpecificSetView extends React.Component {
  constructor(props) {
    super(props);
    //this.setName = this.props.location.state
    this.state = {
      images: [],
    };
    this.classes = makeStyles((theme) => ({
      root: {
        backgroundColor: theme.palette.background.dark,
        minHeight: '100%',
        paddingBottom: theme.spacing(3),
        paddingTop: theme.spacing(3)
      }
    }));
  }

  componentDidMount(){
    console.log(this.setName)
    fetch("http://127.0.0.1:5000/collection/images/?company=nike&set=arnav")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            images: result
          });
        },
        (error) => {
          this.setState({
            images: []
          });
        }
      )
  }

  render() {
    return (
      <Page
      className={this.classes.root}
      title="Set Images"
      >
      <Container maxWidth={false}>
        <Toolbar />
        <Box mt={3}>
          <Results images={this.state.images} />
        </Box>
      </Container>
    </Page>
    )
  }
}

export default SpecificSetView;
