import { AppBar, Box, Drawer, IconButton, Link, Toolbar, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import MenuIcon from "@mui/icons-material/Menu"
import { useState } from "react";


const PrimaryAppBar = () => {
    const [sideMenu, setSideMenu] = useState(false); 
    const theme = useTheme();

    const toggleDrawer = (open: boolean) =>
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        (event: React.MouseEvent) => {
            setSideMenu(open);
        };

    return(
        <AppBar sx = {{ zIndex:(theme) => theme.zIndex.drawer + 2, backgroundColor: theme.palette.background.default, borderBottom: `2px solid ${theme.palette.divider}`}}>
            <Toolbar variant="dense" sx={{height: theme.primaryAppBar.height, minHeight: theme.primaryAppBar.height}}>
                <Box sx={{display: {xs: "block", sm: "none"}}}>
                    <IconButton color="inherit" aria-label="open drawer" onClick={toggleDrawer(true)} edge="start" sx={{mr:2}}>
                        <MenuIcon />
                    </IconButton>
                </Box>

                <Drawer anchor="left" open={sideMenu} onClose={toggleDrawer(false)}>
                    {[...Array(100)].map((_, i) => (
                        <Typography key={i} paragraph>
                            {i + 1}
                        </Typography>
                    ))}
                </Drawer>
                
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