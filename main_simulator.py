from world import *
from simulation import *

def main():

    simul = Simulation()

    field = SoccerField()
    pygame.display.set_icon(field.robofei_logo_scaled)


    #Main loop
    while 1:

        #Process events
        simul.perform_events()

        #Update object positions
        simul.update_pos()

        #check for collisions
        simul.check_collision()

        #update soccer field
        field.draw_soccer_field()

        #Draw robots, ball and update the current frame
        simul.display_update()

        #Pause for the next frame
        clock.tick(60)

    #Close window and exit
    #pygame.quit()

#Call the main function, start up the simulation
if __name__ == "__main__":
    main()