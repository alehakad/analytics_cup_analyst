import plotly.graph_objects as go


class FootballPitch:
    """
    FootballPitch draws a football (soccer) pitch using Plotly.

    Parameters:
        width (float): Length of the pitch in meters (default 120)
        height (float): Width of the pitch in meters (default 80)
        penalty_box_height (float): Height of the penalty box (default 44)
        penalty_box_width (float): Width of the penalty box (default 18)
        penalty_x (float): Distance from the goal line to the penalty spot (default 12)
        goal_box_height (float): Height of the goal box (default 20)
        goal_box_width (float): Width of the goal box (default 6)
        goal_width (float): Width of the goal (default 2.4)
        goal_height (float): Height of the goal (default 8)
        central_radius (float): Radius of the center circle (default 10)

    Methods:
        draw(): Returns a Plotly Figure object representing the football pitch.
    """
    def __init__(self, width=120, height=80, penalty_box_height=44, penalty_box_width=18, penalty_x=12, goal_box_height=20, goal_box_width=6, goal_width=2.4, goal_height=8, central_radius=10):
        self.width = width
        self.height = height
        self.penalty_box_height = penalty_box_height
        self.penalty_box_width = penalty_box_width
        self.penalty_x = penalty_x
        self.goal_box_height = goal_box_height
        self.goal_box_width = goal_box_width
        self.goal_width = goal_width
        self.goal_height = goal_height
        self.central_radius = central_radius

    def draw(self):

        central_x, central_y = self.width/2, self.height/2
        
        penalty_box_left_up = (0, central_y-self.penalty_box_height/2)
        penalty_box_left_down = (self.penalty_box_width, central_y+self.penalty_box_height/2)

        penalty_box_right_up = (self.width, central_y-self.penalty_box_height/2)
        penalty_box_right_down = (self.width-self.penalty_box_width, central_y+self.penalty_box_height/2)
        
        goal_box_left_up = (0, central_y-self.goal_box_height/2)
        goal_box_left_down = (self.goal_box_width, central_y+self.goal_box_height/2)

        goal_box_right_up = (self.width, central_y-self.goal_box_height/2)
        goal_box_right_down = (self.width-self.goal_box_width, central_y+self.goal_box_height/2)

        penalty_left = (self.penalty_x, central_y)
        penalty_right = (self.width-self.penalty_x, central_y)

        goal_left_up = (-self.goal_width, central_y-self.goal_height/2)
        goal_left_down = (0, central_y+self.goal_height/2)

        goal_right_up = (self.width+self.goal_width, central_y-self.goal_height/2)
        goal_right_down = (self.width, central_y+self.goal_height/2)
        
        # Create figure for football pitch
        fig = go.Figure()
        
        # Pitch outline (120x80)
        fig.add_shape(type="rect", x0=0, y0=0, x1=self.width, y1=self.height, line=dict(color="green", width=3), layer="between")
        
        # Center line
        fig.add_shape(type="line", x0=central_x, y0=0, x1=central_x, y1=self.height, line=dict(color="green", width=3), layer="between")
        
        # Center circle
        fig.add_shape(type="circle", x0=central_x-self.central_radius, y0=central_y-self.central_radius, x1=central_x+self.central_radius, y1=central_y+self.central_radius, line=dict(color="green", width=3), layer="between")
        
        # Left penalty box (big rectangle)
        fig.add_shape(type="rect", x0=penalty_box_left_up[0], y0=penalty_box_left_up[1], x1=penalty_box_left_down[0], y1=penalty_box_left_down[1], line=dict(color="green", width=3), layer="between")
        
        # Right penalty box (big rectangle)
        fig.add_shape(type="rect", x0=penalty_box_right_up[0], y0=penalty_box_right_up[1], x1=penalty_box_right_down[0], y1=penalty_box_right_down[1], line=dict(color="green", width=3), layer="between")
        
        # Left goal box (small rectangle)
        fig.add_shape(type="rect", x0=goal_box_left_up[0], y0=goal_box_left_up[1], x1=goal_box_left_down[0], y1=goal_box_left_down[1], line=dict(color="green", width=3), layer="between")
        
        # Right goal box (small rectangle)
        fig.add_shape(type="rect", x0=goal_box_right_up[0], y0=goal_box_right_up[1], x1=goal_box_right_down[0], y1=goal_box_right_down[1], line=dict(color="green", width=3), layer="between")
        
        # penalty spots
        fig.add_trace(go.Scatter(
            x=[penalty_left[0]],
            y=[penalty_left[1]],
            mode='markers',
            marker=dict(color='green', size=7),
            name="Penalty Point",
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[penalty_right[0]],
            y=[penalty_right[1]],
            mode='markers',
            marker=dict(color='green', size=7),
            name="Penalty Point",
            showlegend=False
        ))
        
        #central point
        fig.add_trace(go.Scatter(
            x=[central_x],
            y=[central_y],
            mode='markers',
            marker=dict(color='green', size=7),
            name="Center Point",
            showlegend=False
            
        ))
        
        # goals
        fig.add_shape(type="rect", x0=goal_left_up[0], y0=goal_left_up[1], x1=goal_left_down[0], y1=goal_left_down[1], line=dict(color="green", width=3))
        fig.add_shape(type="rect", x0=goal_right_up[0], y0=goal_right_up[1], x1=goal_right_down[0], y1=goal_right_down[1], line=dict(color="green", width=3))
        
        # Left penalty arc (half-circle)
        fig.add_shape(type="path",
                      path="M 18 50 Q 24 38, 18 30",  # Semi-circle shape
                      line=dict(color="green", width=3),layer="between")
        
        # Right penalty arc (half-circle)
        fig.add_shape(type="path",
                      path="M 102 50 Q 95 38, 102 30",  # Semi-circle shape
                      line=dict(color="green", width=3),layer="between")
        
        # Update layout settings
        fig.update_layout(width=1200, height=800, plot_bgcolor="white", showlegend=True, autosize=True)
        
        # Set axes to not show grid lines
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(autorange="reversed", range=[80, 0], showgrid=False, zeroline=False)
        
        return fig

