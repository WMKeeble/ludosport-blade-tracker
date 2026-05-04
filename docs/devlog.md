## 2026-05-01
Initialised the repo. First goal is to get some archived livestream footage and isolate the blades.

Key assumption: That the illuminated blades can be isolated primarily by brightness thresholding.

## 2026-05-02
Got basic blade detection working -ish. Lots of refinement still required to make it reliable.

Brightness thresholding does not work - the blades are notably less bright than skylights, ceiling lights, etc. However, colour thresholding shows some promise. Have detected basic blue blades with some condfidence.

Currently working on morphology. I suspect later I will need to use more sophisticated methods - detecting athlete's skeletons to pick out the blade, especially for other blade colours.

## 20206-05-04

