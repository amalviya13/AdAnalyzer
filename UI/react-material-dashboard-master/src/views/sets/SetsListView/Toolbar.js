import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import Input from "@material-ui/core/Input";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";
import { Link } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  SvgIcon,
  makeStyles
} from '@material-ui/core';
import { Search as SearchIcon } from 'react-feather';
import useMediaQuery from '@material-ui/core/useMediaQuery';


const Toolbar = ({ className, ...rest }) => {

  function refreshPage() {
    window.location.reload(false);
  }

  const useStyles = makeStyles((theme) => ({
    root: {},
    dialogPaper: { 
      minHeight: '80vh',
      maxHeight: '80vh'
    },
    addSet: {
      marginRight: theme.spacing(1),
      marginTop: theme.spacing(1)
    }
  }));

  const classes = useStyles();
  const [description, setDescription] = useState("");
  const [open, setOpen] = useState(false)

  return (
    <div
      className={clsx(classes.root, className)}
      {...rest}
    >
      <Box
        display="flex"
        justifyContent="flex-end"
      >
        <Button
          color="primary"
          variant="contained"
          className={classes.addSet}
          onClick={() => setOpen(true)}
        >
          Add set
        </Button>
        <Dialog
          open={open}
        >
          <DialogTitle id="max-width-dialog-title">Optional sizes</DialogTitle>
          { <FormControl fullWidth>
            <InputLabel htmlFor="CSV">CSV</InputLabel>
            <Input
              id="comment"
              onChange={event => setDescription(event.target.value)}
            />                      
          </FormControl> }
          <div>
            <Button
              onClick={refreshPage}
              m={5}
            >
              Submit
            </Button>
            <Button
              m={5}
              onClick={refreshPage}
            >
              Cancel
            </Button>
          </div>
        </Dialog>
      </Box>
    </div>
  );
};

Toolbar.propTypes = {
  className: PropTypes.string
};

export default Toolbar;
