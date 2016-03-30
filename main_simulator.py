from world import *
from simulation import *

def main():

    screen = Screen()
    screen.start_simulation()


    simul = Simulation(screen)


    field = SoccerField(screen)

    simul.field = field

    pygame.display.set_icon(field.robofei_logo)


    #Main loop
    while True:

        #Process events
        simul.perform_events()

        #Update object positions checking for collisions
        simul.update_pos()


        #update soccer field
        field.draw_soccer_field()

        #Ball searching
        #simul.searching()

        #Draw robots, ball and update the current frame
        simul.display_update()

        #Pause for the next frame
        screen.clock.tick(60)


    #Close window and exit
    #pygame.quit()

#Call the main function, start up the simulation
if __name__ == "__main__":
    main()