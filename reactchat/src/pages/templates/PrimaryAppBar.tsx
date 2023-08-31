import { AppBar, Box, IconButton, Link, Toolbar, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import MenuIcon from "@mui/icons-material/Menu"


const PrimaryAppBar = () => {
    const theme = useTheme();
    return(
        <AppBar sx = {{backgroundColor: theme.palette.background.default, borderBottom: `2px solid ${theme.palette.divider}`}}>
            <Toolbar variant="dense" sx={{height: theme.primaryAppBar.height, minHeight: theme.primaryAppBar.height}}>
                <Box>
                    <IconButton>
                        <MenuIcon />
                    </IconButton>
                </Box>
                <Link href="/" underline="none" color="inherit"> 
                    <Typography 
                        variant="h4" 
                        noWrap 
                        component="div" sx={{display:{fontWeight: 700, letterSpacing: "=-0.5px" } } }>
                        DJChat
                    </Typography>
                </Link>
            </Toolbar>
        </AppBar>
    );
};
export default PrimaryAppBar;