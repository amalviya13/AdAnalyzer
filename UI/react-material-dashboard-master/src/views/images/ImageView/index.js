import React from 'react';
import {
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import Pie from './Pie';
import Histogram from './Histogram';
import Top5Bar from './Top5Bar';


const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

const Dashboard = () => {
  const classes = useStyles();

  return (
    <Page
      className={classes.root}
      title="Dashboard"
    >
      <Container maxWidth={false}>
        <Grid
          container
          spacing={3}
        >
          <Grid
            item
          >
            <Pie />
          </Grid>
          <Grid
            item
          >
            <Histogram />
          </Grid>
        </Grid>
        <Grid>
          <Grid>
            <Top5Bar />
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
};

export default Dashboard;
