import React, { useState } from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import moment from 'moment';
import PerfectScrollbar from 'react-perfect-scrollbar';
import {
  Avatar,
  Box,
  Card,
  Checkbox,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
  Typography,
  makeStyles
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {},
  avatar: {
    marginRight: theme.spacing(2)
  }
}));

const Results = ({ className, images, ...rest }) => {
  const classes = useStyles();
  const [selectedImages, setSelectedImages] = useState([]);
  const [limit, setLimit] = useState(10);
  const [page, setPage] = useState(0);

  const handleSelectAll = (event) => {
    let newSelectedImages;

    if (event.target.checked) {
      newSelectedImages = images.map((image) => image);
    } else {
      newSelectedImages = [];
    }

    setSelectedImages(newSelectedImages);
  };

  const handleSelectOne = (event, imageName) => {
    const selectedIndex = selectedImages.indexOf(imageName);
    let newSelectedImages = [];

    if (selectedIndex === -1) {
      newSelectedImages = newSelectedImages.concat(selectedImages, imageName);
    } else if (selectedIndex === 0) {
      newSelectedImages = newSelectedImages.concat(selectedImages.slice(1));
    } else if (selectedIndex === selectedImages.length - 1) {
      newSelectedImages = newSelectedImages.concat(selectedImages.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelectedImages = newSelectedImages.concat(
        selectedImages.slice(0, selectedIndex),
        selectedImages.slice(selectedIndex + 1)
      );
    }

    setSelectedImages(newSelectedImages);
  };

  const handleLimitChange = (event) => {
    setLimit(event.target.value);
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };

  return (
    <Card
      className={clsx(classes.root, className)}
      {...rest}
    >
      <PerfectScrollbar>
        <Box minWidth={1050}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell padding="checkbox">
                  <Checkbox
                    checked={selectedImages.length === images.length}
                    ƒcustomer
                    ="primary"
                    indeterminate={
                      selectedImages.length > 0
                      && selectedImages.length < images.length
                    }
                    onChange={handleSelectAll}
                  />
                </TableCell>
                <TableCell>
                  Image Name
                </TableCell>
                <TableCell>
                  Date Added
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {images.slice(page*limit, (page+1)*limit).map((image) => (
              <TableRow
                  hover
                  key={image}
                  selected={selectedImages.indexOf(image) !== -1}
                >   
                <TableCell>
                  <Checkbox
                    checked={selectedImages.indexOf(image) !== -1}
                    onChange={(event) => handleSelectOne(event, image)}
                    value="true"
                  />
                </TableCell>
                <TableCell>
                  <Box
                      alignItems="center"
                      display="flex"
                    >
                      <Avatar
                        className={classes.avatar}
                        src={image}
                      >
                      </Avatar>
                      <Typography
                        color="textPrimary"
                        variant="body1"
                      >
                        {image}
                      </Typography>
                    </Box>
                </TableCell>            
                <TableCell>
                  {image}
                </TableCell>
              </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </PerfectScrollbar>
      <TablePagination
        component="div"
        count={images.length}
        onChangePage={handlePageChange}
        onChangeRowsPerPage={handleLimitChange}
        page={page}
        rowsPerPage={limit}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Card>
  );
};

Results.propTypes = {
  className: PropTypes.string,
  images: PropTypes.array.isRequired
};

export default Results;
