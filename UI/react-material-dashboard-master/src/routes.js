import React from 'react';
import { Navigate } from 'react-router-dom';
import DashboardLayout from 'src/layouts/DashboardLayout';
import MainLayout from 'src/layouts/MainLayout';
import AccountView from 'src/views/account/AccountView';
import SetListView from 'src/views/sets/SetsListView';
import DashboardView from 'src/views/reports/DashboardView';
import ImageView from 'src/views/images/ImageView';
import LoginView from 'src/views/auth/LoginView';
import NotFoundView from 'src/views/errors/NotFoundView';
import RegisterView from 'src/views/auth/RegisterView';
import SettingsView from 'src/views/settings/SettingsView';
import SpecificSetView from 'src/views/specificSet/SpecificSetView'

const routes = [
  {
    path: 'app',
    element: <DashboardLayout />,
    children: [
      { path: 'account', element: <AccountView /> },
      { path: 'dashboard/:setName', element: <DashboardView /> },
      { path: 'collections', element: <SetListView />},
      { path: 'settings', element: <SettingsView /> },
      { path: 'specificSet/:setName', element: <SpecificSetView />},
      { path: 'image', element: <ImageView />}
    ]
  },
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { path: 'login', element: <LoginView /> },
      { path: 'register', element: <RegisterView /> },
      { path: '404', element: <NotFoundView /> },
      { path: '/', element: <Navigate to="/app/dashboard" /> },
      { path: '*', element: <Navigate to="/404" /> }
    ]
  }
];

export default routes;
