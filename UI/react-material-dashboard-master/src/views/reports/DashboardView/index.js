import React from "react";
import {
  useParams
} from "react-router-dom";
import {
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import Pie from './Pie';
import Histogram from './Histogram';
import Top5Bar from './Top5Bar';
import WarmCool from './WarmCool';
import TopSets from './TopSets';

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
  const params = useParams();
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
            <Pie setName={params.setName} company="nike"/>
          </Grid>
          <Grid
            item
          >
            <Histogram setName={params.setName} company="nike"/>
          </Grid>
        </Grid>
        <Grid
          container
          spacing={5}
        >
          <Grid
            item
          >
            <Top5Bar setName={params.setName} company="nike"/>
          </Grid>
          <Grid
            item
          >
            <WarmCool setName={params.setName} company="nike"/>
          </Grid>
        </Grid>
        <Grid
          container
          spacing={5}
        >
          <Grid
            item
          >
            <TopSets setName={params.setName} company="nike"/>
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
};

export default Dashboard;
