"""
This module provides SimWindow, a class for displaying the status of a collection of segments and sites the map of a simulation.

Requirements
------------
Package dearpygui which can be installed via PIP.
Package numpy which can be installed via PIP.
Python 3.9 or higher.

An example of usage is offered if the code is run as main


Notes
-----
This module is provided as material for the phase 1 project for DM857, DS830 (2024). 

The code is adapted from:
https://github.com/BilHim/trafficSimulator
"""

import dearpygui.dearpygui as dpg
from typing import List,Tuple
import numpy as np
import random
class SimWindow:
    def __init__(self,draw_bridges:bool=False):
        """
        Each instance of this class maintains a window 
        to display the status of a given collection of edges forming the map of a simulation.
        The convention used assumes that each segment is of width 5.

        Parameters:
        ---------- 
        draw_bridges: bool Optional
        This function show crossing (bridges) that do not correspond to segments' junctions

        """

        self.zoom = 2
        self.offset = (-200, -100)

        self.old_offset = (0, 0)
        self.is_dragging = False
        self.zoom_speed = 1
        self.draw_bridges = draw_bridges
        
        self._setup()
        self._setup_themes()
        self._create_windows()
        self._create_handlers()
        self._resize_windows()
        self.segments = []
        self.vehicles = []
        self.caracol = []
        self.in_gates = []
        self.out_gates = []
        
    def set_roads(self,segs:list[(int,int)]):
        """
        defines the map 

        Parameters:
        ---------- 
        segs: List[((int,int),(int,int))]
        The segs list requires to identify the begining and the end of each segment.
        Note: The segments are now directed, they identify a versus from the beginning to the end.
        No check is implemented to make sure the segments are connected.
        
         gates: List[(int,int))]
        The gates list will act as source of cars and must be in correspondence of the beggining of a segment
        No check is implemented to make sure that the position is correct.
        """
        self.segments = segs.copy()
       
    def set_in_gates(self,gates:list[(int,int)]):
        """
        Identifies on the map entrances to the highway
        
        Parameters:
        ---------- 
        gates: List[(int,int))]
        The gates list will act as source of cars and must be in correspondence of the beggining of a segment
        No check is implemented to make sure that the position is correct.
        """
        self.in_gates = gates.copy()
        
    def set_out_gates(self,gates:list[(int,int)]):
        """
        Identifies on the map the exits to the highway
        
        Parameters:
        ---------- 
        gates: List[(int,int))]
        The gates list will act as source of cars and must be in correspondence of the end of a segment
        No check is implemented to make sure that the position is correct.
        """     
        self.out_gates = gates.copy()
        
    def _setup(self):
        dpg.create_context()
        dpg.create_viewport(title="Main Window", width=1280, height=720)
        dpg.setup_dearpygui()


    def _setup_themes(self):
        with dpg.theme() as global_theme:

            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (90, 90, 95))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 91, 140))
            with dpg.theme_component(dpg.mvInputInt):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (90, 90, 95), category=dpg.mvThemeCat_Core)

        dpg.bind_theme(global_theme)

      #  dpg.show_style_editor()
    
    def _create_windows(self):
        dpg.add_window(
            tag="MainWindow",
            label="Landscape",
            no_close=True,
            no_collapse=True,
            no_resize=False,
            no_move=False
        )
        
        dpg.add_draw_node(tag="OverlayCanvas", parent="MainWindow")
        dpg.add_draw_node(tag="Canvas", parent="MainWindow")

        with dpg.window(
            tag="ControlsWindow",
            label="Controls",
            no_close=True,
            no_collapse=True,
            no_resize=True,
            no_move=True
        ):
            with dpg.collapsing_header(label="Camera Control", default_open=True):
                dpg.add_slider_float(tag="ZoomSlider", label="Zoom", min_value=0.1, max_value=100, default_value=self.zoom,callback=self._set_offset_zoom)            
                with dpg.group():
                    dpg.add_slider_float(tag="OffsetXSlider", label="X Offset", min_value=-100, max_value=100, default_value=self.offset[0], callback=self._set_offset_zoom)
                    dpg.add_slider_float(tag="OffsetYSlider", label="Y Offset", min_value=-100, max_value=100, default_value=self.offset[1], callback=self._set_offset_zoom)

    def _set_offset_zoom(self):
        self.zoom = dpg.get_value("ZoomSlider")
        self.offset = (dpg.get_value("OffsetXSlider"), dpg.get_value("OffsetYSlider"))
           

    def _mouse_down(self):
        if not self.is_dragging:
            if dpg.is_item_hovered("MainWindow"):
                self.is_dragging = True
                self.old_offset = self.offset
        
    def _mouse_drag(self, sender, app_data):
        if self.is_dragging:
            self.offset = (
                self.old_offset[0] + app_data[1]/self.zoom,
                self.old_offset[1] + app_data[2]/self.zoom
            )

    def _mouse_release(self):
        self.is_dragging = False

    def _mouse_wheel(self, sender, app_data):
        if dpg.is_item_hovered("MainWindow"):
            self.zoom_speed = 1 + 0.01*app_data

    def _update_inertial_zoom(self, clip=0.005):
        if self.zoom_speed != 1:
            self.zoom *= self.zoom_speed
            self.zoom_speed = 1 + (self.zoom_speed - 1) / 1.05
        if abs(self.zoom_speed - 1) < clip:
            self.zoom_speed = 1

    def _create_handlers(self):
        with dpg.handler_registry():
            dpg.add_mouse_down_handler(callback=self._mouse_down)
            dpg.add_mouse_drag_handler(callback=self._mouse_drag)
            dpg.add_mouse_release_handler(callback=self._mouse_release)
            dpg.add_mouse_wheel_handler(callback=self._mouse_wheel)
        dpg.set_viewport_resize_callback(self._resize_windows)

    def _resize_windows(self):
        width = dpg.get_viewport_width()
        height = dpg.get_viewport_height()

        dpg.set_item_width("ControlsWindow", 300)
        dpg.set_item_height("ControlsWindow", height-38)
        dpg.set_item_pos("ControlsWindow", (0, 0))

        dpg.set_item_width("MainWindow", width-315)
        dpg.set_item_height("MainWindow", height-38)
        dpg.set_item_pos("MainWindow", (300, 0))
    
    def show(self, updatecar=None):
        """
        Handle to show the simulation interface.
        Updatecar is a handle to move the cars on the road.
        It requires to be define as a function.
        
        Parameters:
        ---------- 

        updatecar: Optional
        A function to update the cars position at each iteration define through the interface:
        def updatecar(carposition:List[(int,int)],carcolours:List[(int,int,int)])->None:
        
 
        """
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            self._render_loop(updatecar)
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

    def _update_offset_zoom_slider(self):
        dpg.set_value("ZoomSlider", self.zoom)
        dpg.set_value("OffsetXSlider", self.offset[0])
        dpg.set_value("OffsetYSlider", self.offset[1])

    @property
    def _canvas_width(self):
        return dpg.get_item_width("MainWindow")

    @property
    def _canvas_height(self):
        return dpg.get_item_height("MainWindow")

    def _draw_bg(self, color=(250, 250, 250)):
        dpg.draw_rectangle(
            (-10, -10),
            (self._canvas_width+10, self._canvas_height+10), 
            thickness=0,
            fill=color,
            parent="OverlayCanvas"
        )

    def _draw_axes(self, opacity=80):
        x_center, y_center = self._to_screen(0, 0)

        dpg.draw_line(
            (-10, y_center),
            (self._canvas_width+10, y_center),
            thickness=2, 
            color=(0, 0, 0, opacity),
            parent="OverlayCanvas"
        )
        dpg.draw_line(
            (x_center, -10),
            (x_center, self._canvas_height+10),
            thickness=2,
            color=(0, 0, 0, opacity),
            parent="OverlayCanvas"
        )

    
    def _draw_grid(self, unit=10, opacity=50):
        x_start, y_start = self._to_world(0, 0)
        x_end, y_end = self._to_world(self._canvas_width, self._canvas_height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        for i in range(n_x, m_x):
            dpg.draw_line(
                self._to_screen(unit*i, y_start - 10/self.zoom),
                self._to_screen(unit*i, y_end + 10/self.zoom),
                thickness=1,
                color=(0, 0, 0, opacity),
                parent="OverlayCanvas"
            )

        for i in range(n_y, m_y):
            dpg.draw_line(
                self._to_screen(x_start - 10/self.zoom, unit*i),
                self._to_screen(x_end + 10/self.zoom, unit*i),
                thickness=1,
                color=(0, 0, 0, opacity),
                parent="OverlayCanvas"
            )


    def _to_screen(self, x, y):
        return (
            self._canvas_width/2 + (x + self.offset[0] ) * self.zoom,
            self._canvas_height/2 + (y + self.offset[1]) * self.zoom
        )

    def _to_world(self, x, y):
        return (
            (x - self._canvas_width/2) / self.zoom - self.offset[0],
            (y - self._canvas_height/2) / self.zoom - self.offset[1] 
        )

    def _apply_transformation(self):
        screen_center = dpg.create_translation_matrix([self._canvas_width/2, self._canvas_height/2, -0.01])
        translate = dpg.create_translation_matrix(self.offset)
        scale = dpg.create_scale_matrix([self.zoom, self.zoom])
        dpg.apply_transform("Canvas", screen_center*scale*translate)


    def _draw_segments(self):
        for segment in self.segments:
            dpg.draw_polyline(segment, color=(180, 180, 220), thickness=5*self.zoom, parent="Canvas")
            dpg.draw_circle(segment[0],2.5*self.zoom, color=(220, 220, 220), fill=(220, 220, 220), thickness=0, parent="Canvas")
            dpg.draw_circle(segment[1],2.5*self.zoom, color=(220, 220, 220), fill=(220, 220, 220), thickness=0, parent="Canvas")

    def _draw_bridge_intersections(self):
        bridges=[]
        for i in range(len(self.segments)):
            pp= self.segments[i]
            x0=pp[0][0]
            x1=pp[1][0]
            y0=pp[0][1]
            y1=pp[1][1]
            dx = x0 - x1
            dy = y0 - y1
            for j in range(i+1,len(self.segments)):
                pp= self.segments[j]
                X0=pp[0][0]
                X1=pp[1][0]
                Y0=pp[0][1]
                Y1=pp[1][1]
                dX = X0 - X1
                dY = Y0 - Y1

                det = dx*dY -dy*dX
                dt1 = (dY *(x0 - X1) - dX *(y0 - Y1))
                dt2 = (dx *(Y0 - y1) - dy* (X0 - x1) )
                if(det!=0):
                    t1 = 1/det * dt1
                    t2 = 1/det * dt2
                    if (t1 >=0  )  and  (t1 <= 1 ) and (t2 >=  0)  and  (t2 <= 1 ):
                        dd = np.sqrt(dx**2 + dy**2)
                        DD = np.sqrt(dX**2 + dY**2)
                        if ( ( t1 >= 1/(dd) ) and ( t1 <= 1-1/(dd) ) ) or  ( ( t2 >= 1/(DD) ) and ( t2 <= 1-1/(DD) ) ):
                            bridges.append(((x1 - x0)*t1 + x0, (y1 - y0) * t1 + y0))
                else:
                    if(dt1 ==0 ) and (dt2 == 0):
                        if (self.segments[i][0][0] == self.segments[i][1][0]):
                            s0=[self.segments[i][0][1],self.segments[i][1][1]]
                            s1=[self.segments[j][0][1],self.segments[j][1][1]]
                            p0 = [self.segments[i][0][1],self.segments[i][1][1],self.segments[j][0][1],self.segments[j][1][1]]
                        if (self.segments[i][0][1] == self.segments[i][1][1]):
                            s0=[self.segments[i][0][0],self.segments[i][1][0]]
                            s1=[self.segments[j][0][0],self.segments[j][1][0]]
                            p0 = [self.segments[i][0][0],self.segments[i][1][0],self.segments[j][0][0],self.segments[j][1][0]]
                        p0.sort()
                        s0.sort()
                        s1.sort()
                        
                        if (p0[0:2]==s0) or (p0[0:2]==s1):
                            continue
                        
                        p1 = p0[1:3]
                        if (self.segments[i][0][0] == self.segments[i][1][0]):
                            for k in range(p1[0],p1[1]):
                                if(k!=self.segments[i][0][1]):
                                    bridges.append((self.segments[i][0][0],k))             
                        if (self.segments[i][0][1] == self.segments[i][1][1]):
                            for k in range(p1[0],p1[1]):
                                if(k!=self.segments[i][0][0]):
                                    bridges.append((k,self.segments[i][0][1]))             
        for wp in bridges:
            dpg.draw_circle(wp,2.5*self.zoom, color=(0, 0, 0), fill=(0, 0, 0), thickness=0, parent="Canvas")

  
    def _draw_vehicles(self):
        for id in range(len(self.vehicles)):
            dpg.draw_circle(self.vehicles[id],2.5*self.zoom, color=self.caracol[id], fill=self.caracol[id], thickness=0, parent="Canvas")

    def _draw_gates(self):
        for gate in self.in_gates:
            p1=(np.array(gate) - np.array((5,5))).tolist()
            p2=(np.array(gate) + np.array((5,5))).tolist()
            dpg.draw_rectangle(p1,p2, color=(124,252,0), fill=(24,252,0), thickness=0, parent="Canvas")

        for gate in self.out_gates:
            p1=(np.array(gate) - np.array((5,5))).tolist()
            p2=(np.array(gate) + np.array((5,5))).tolist()
            dpg.draw_rectangle(p1,p2, color=(0,0,139), fill=(0,0,139), thickness=0, parent="Canvas")


    def _render_loop(self,updatecar):
        ## Events
        self._update_inertial_zoom()
        self._update_offset_zoom_slider()

       ## Remove old drawings
        dpg.delete_item("OverlayCanvas", children_only=True)
        dpg.delete_item("Canvas", children_only=True)
       
       ## New drawings
        self._draw_bg()
        self._draw_axes()
        self._draw_grid(unit=10)
        self._draw_grid(unit=50)
        self._draw_segments()
        self._draw_gates()
        self._draw_vehicles()
        if self.draw_bridges :
            self._draw_bridge_intersections()

       ## Apply transformations
        self._apply_transformation()

       ## Update simulation
        if (updatecar!=None):
            updatecar(self.vehicles,self.caracol)


    

if __name__ == "__main__": 
    #Setup of the interface
    ms = SimWindow(draw_bridges=True)
    

    segs = [((0,0),(100,0)), ((100,0), (100,100)), ((100,100),(0, 100)), ((0,100),(0,0)),
            ((0,-100),(0,0)), ((200,100),(100,100))]
    ms.set_roads(segs)
 
    in_gates=[(200,100)]
    ms.set_in_gates(in_gates)

    out_gates=[]
    out_gates.append((0, -100))
    ms.set_out_gates(out_gates)

    #show the window
    ms.show()
