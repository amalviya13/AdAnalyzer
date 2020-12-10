import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { Link } from 'react-router-dom';
import {
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Grid,
  Typography,
  makeStyles
} from '@material-ui/core';
import PermMediaSharpIcon from '@material-ui/icons/PermMediaSharp';
import AssessmentIcon from '@material-ui/icons/Assessment';
const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column'
  },
  statsItem: {
    alignItems: 'center',
    display: 'flex'
  },
  statsIcon: {
    marginRight: theme.spacing(1)
  }
}));

const SetCard = ({ className, product, ...rest }) => {
  const classes = useStyles();

  return (
    <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <CardContent>
        <Box
          display="flex"
          justifyContent="center"
          mb={3}
        >
          <Avatar
            alt="Product"
            variant="square"
          />
        </Box>
        <Typography
          align="center"
          color="textPrimary"
          gutterBottom
          variant="h4"
        >
          {product.set}
        </Typography>
      </CardContent>
      <Box flexGrow={1} />
      <Divider />
      <Box p={2}>
        <Grid
          container
          justify="space-between"
          spacing={2}
        >
          <Grid
            className={classes.statsItem}
            item
          >
            <PermMediaSharpIcon/>
            <Button
              display="inline"
              
              component={Link} to=
                {{
                  pathname: "/app/specificSet/" + product.set,
                  state: { query : product.set }
                }}>
                <Typography
                  display="inline"
                >
                  {product.num_images}
                  {' '}
                  Images
                </Typography>
            </Button>
            <AssessmentIcon/>
            <Button
              display="inline"
              component={Link} to=
                {{
                  pathname: "/app/dashboard/" + product.set,
                  state: { "name": product.set }
                }}
              >
                <Typography
                  display="inline"
                >
                  Set Analytics
                </Typography>
            </Button>
          </Grid>
          <Grid
            className={classes.statsItem}
            item
          >
          </Grid>
        </Grid>
      </Box>
    </Card>
  );
};

SetCard.propTypes = {
  className: PropTypes.string,
  product: PropTypes.object.isRequired
};

export default SetCard;
