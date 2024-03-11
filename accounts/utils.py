def detectUser(user):
  if user.role == 1:
    redirectUrl ='dashboardVendor'
  elif  user.role == 2:
    redirectUrl ='dashboardCustomer'
  elif  user.role == None and user.is_superadmin:
    redirectUrl ='/admin'

  return redirectUrl


