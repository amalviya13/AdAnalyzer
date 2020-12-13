import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import Results from './Results';
import Toolbar from './Toolbar';
import {
  useParams
} from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

const SpecificSetView = () => {
  const classes = useStyles();
  const params = useParams();
  let [images, setImages] = useState([""]);

  useEffect(() => {
      fetch("http://127.0.0.1:5000/collection/images/?company=nike&set=" + params.setName)
      .then(res => res.json())
      .then(
        (result) => {
          images = result;
          setImages(result)
        },
        (error) => {
          this.setState({
            images: [""]
          });
        }
      )
    }, [])
    
  return (
    <Page
        className={classes.root}
      title="Set Images"
      >
      <Container maxWidth={false}>
        <Toolbar />
        <Box mt={3}>
          <Results images={images} />
        </Box>
      </Container>
    </Page>
  );
};

export default SpecificSetView;
