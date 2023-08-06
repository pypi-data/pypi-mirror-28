//vertices
Point(201)= {168.972917659,168.972917659,-6.3921811797,5};
Point(202)= {343.027082341,168.972917659,-6.3921811797,5};
Point(203)= {343.027082341,343.027082341,-6.3921811797,5};
Point(204)= {168.972917659,343.027082341,-6.3921811797,5};
Point(205)= {168.972917659,168.972917659,-4.13384916961,5};
Point(206)= {343.027082341,168.972917659,-4.13384916961,5};
Point(207)= {343.027082341,343.027082341,-4.13384916961,5};
Point(208)= {168.972917659,343.027082341,-4.13384916961,5};

//lines
Line(201)= {201,202};
Line(202)= {202,203};
Line(203)= {203,204};
Line(204)= {204,201};
Line(205)= {205,206};
Line(206)= {206,207};
Line(207)= {207,208};
Line(208)= {208,205};
Line(209)= {201,205};
Line(210)= {202,206};
Line(211)= {203,207};
Line(212)= {204,208};

//arcs

//lineLoops
Line Loop(201)= {201,202,203,204};
Line Loop(202)= {205,206,207,208};
Line Loop(203)= {-201,209,205,-210};
Line Loop(204)= {-202,210,206,-211};
Line Loop(205)= {-203,211,207,-212};
Line Loop(206)= {-204,212,208,-209};

//ruledSurfaces
Ruled Surface(201)= {201};
Ruled Surface(202)= {202};
Ruled Surface(203)= {203};
Ruled Surface(204)= {204};
Ruled Surface(205)= {205};
Ruled Surface(206)= {206};

//surfaceLoops
Surface Loop(201)= {201,202,203,204,205,206};

//volumes
Volume(201)= {201};

//Boundary Layer
Field[2] = BoundaryLayer;
Field[2].Quads = 0;
Field[2].hfar = 1;
Field[2].hwall_n = 1;
Field[2].hwall_t = 2;
Field[2].thickness = 10;
Field[2].EdgesList = {210, 211,212};
Field[2].AnisoMax = 1000000;
Field[2].IntersectMetrics = 1;
Background Field = 2; 