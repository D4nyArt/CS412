import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from project.models import Exercise, TrainingSchedule, Routine, RoutineItem, WorkoutSession, WorkoutLog

class Command(BaseCommand):
    help = 'Wipes old schedules/logs (keeping exercises) and generates 3 phases for the Admin.'

    def handle(self, *args, **kwargs):
        self.stdout.write("--- STARTING SEED PROCESS ---")

        # 1. GET THE ADMIN USER
        # We grab the first superuser found.
        user = User.objects.filter(is_superuser=True).first()
        
        if not user:
            self.stdout.write(self.style.ERROR("Error: No Admin user found. Please run 'python manage.py createsuperuser' first."))
            return
        
        self.stdout.write(f"- Assigning data to Admin: {user.username}")

        # 2. CLEANUP (RESET)
        # Deleting the Schedule cascades and deletes Routines, Sessions, and Logs.
        # It does NOT delete Exercises.
        count, _ = TrainingSchedule.objects.filter(user=user).delete()
        self.stdout.write(f"- Wiped {count} old objects (Schedules, Routines, Logs) for this user.")
        self.stdout.write("- Existing Exercises preserved.")

        # 3. MAP EXERCISES
        # We need to map the script's required names to your existing DB objects.
        # If your DB is missing "Bench Press", this will create it safely.
        required_exercises = [
            ("Bench Press", "Chest"), ("Squat", "Legs"), ("Deadlift", "Back"),
            ("Overhead Press", "Shoulders"), ("Pull Up", "Back"), ("Dumbbell Curl", "Arms"),
            ("Tricep Extension", "Arms"), ("Lunges", "Legs"), ("Lat Pulldown", "Back"),
            ("Leg Press", "Legs"), ("Incline Bench", "Chest")
        ]
        
        ex_map = {}
        for name, muscle in required_exercises:
            # Try to get it, or create it if missing (Safeguard)
            ex, created = Exercise.objects.get_or_create(name=name, defaults={'muscle_group': muscle})
            ex_map[name] = ex
            if created:
                self.stdout.write(f"  (Note: Created missing exercise '{name}')")

        # BASELINE STRENGTH
        current_strength = {
            "Bench Press": 115.0, "Squat": 155.0, "Deadlift": 185.0, "Overhead Press": 75.0,
            "Pull Up": 0.0, "Dumbbell Curl": 20.0, "Tricep Extension": 30.0, "Lunges": 30.0,
            "Lat Pulldown": 80.0, "Leg Press": 200.0, "Incline Bench": 95.0
        }

        # --- DEFINING THE 3 PHASES ---
        today = timezone.now().date()
        phases = [
            {
                "name": "Spring Foundation",
                "start_offset": 180, "end_offset": 100, 
                "split_type": "FullBody"
            },
            {
                "name": "Summer Shred",
                "start_offset": 100, "end_offset": 40, 
                "split_type": "UpperLower"
            },
            {
                "name": "Winter Bulk",
                "start_offset": 40, "end_offset": 0, 
                "split_type": "PPL"
            }
        ]

        total_sessions = 0

        for phase in phases:
            start_date = today - timedelta(days=phase["start_offset"])
            end_date = today - timedelta(days=phase["end_offset"])
            is_active = (phase["end_offset"] == 0)

            # A. Create Schedule
            schedule = TrainingSchedule.objects.create(
                user=user,
                name=phase["name"],
                start_date=start_date,
                end_date=end_date,
                is_active=is_active
            )
            self.stdout.write(f"\nGenerating Phase: {schedule.name} ({phase['split_type']})")

            # B. Create Routines
            routines = []
            
            if phase["split_type"] == "FullBody":
                r_a = Routine.objects.create(schedule=schedule, name="Full Body A", day_of_week="Monday")
                r_b = Routine.objects.create(schedule=schedule, name="Full Body B", day_of_week="Wednesday")
                routines = [r_a, r_b]
                self.create_items(r_a, [("Squat", 3, 5), ("Bench Press", 3, 8), ("Pull Up", 3, 8)], ex_map)
                self.create_items(r_b, [("Deadlift", 3, 5), ("Overhead Press", 3, 8), ("Lunges", 3, 10)], ex_map)

            elif phase["split_type"] == "UpperLower":
                r_up = Routine.objects.create(schedule=schedule, name="Upper Power", day_of_week="Monday")
                r_low = Routine.objects.create(schedule=schedule, name="Lower Power", day_of_week="Tuesday")
                routines = [r_up, r_low]
                self.create_items(r_up, [("Bench Press", 3, 5), ("Pull Up", 3, 8), ("Dumbbell Curl", 3, 12)], ex_map)
                self.create_items(r_low, [("Squat", 3, 5), ("Leg Press", 3, 10), ("Lunges", 3, 12)], ex_map)

            elif phase["split_type"] == "PPL":
                r_push = Routine.objects.create(schedule=schedule, name="Push", day_of_week="Monday")
                r_pull = Routine.objects.create(schedule=schedule, name="Pull", day_of_week="Wednesday")
                r_legs = Routine.objects.create(schedule=schedule, name="Legs", day_of_week="Friday")
                routines = [r_push, r_pull, r_legs]
                self.create_items(r_push, [("Bench Press", 4, 8), ("Incline Bench", 3, 10), ("Tricep Extension", 3, 15)], ex_map)
                self.create_items(r_pull, [("Deadlift", 3, 5), ("Lat Pulldown", 3, 12), ("Dumbbell Curl", 3, 12)], ex_map)
                self.create_items(r_legs, [("Squat", 4, 6), ("Leg Press", 3, 12), ("Lunges", 3, 12)], ex_map)

            # C. Simulate History
            delta_days = (end_date - start_date).days
            for i in range(delta_days + 1):
                current_day = start_date + timedelta(days=i)
                day_name = current_day.strftime('%A')
                
                todays_routine = None
                for r in routines:
                    if phase["split_type"] == "FullBody":
                        if day_name == "Monday" and r.name == "Full Body A": todays_routine = r
                        if day_name == "Wednesday" and r.name == "Full Body B": todays_routine = r
                        if day_name == "Friday" and r.name == "Full Body A": todays_routine = r
                    elif phase["split_type"] == "UpperLower":
                        if day_name in ["Monday", "Thursday"] and r.name == "Upper Power": todays_routine = r
                        if day_name in ["Tuesday", "Friday"] and r.name == "Lower Power": todays_routine = r
                    elif phase["split_type"] == "PPL":
                        if day_name in ["Monday", "Thursday"] and r.name == "Push": todays_routine = r
                        if day_name in ["Tuesday", "Friday"] and r.name == "Pull": todays_routine = r
                        if day_name in ["Wednesday", "Saturday"] and r.name == "Legs": todays_routine = r

                if todays_routine and random.random() < 0.9:
                    session = WorkoutSession.objects.create(
                        routine=todays_routine,
                        date=current_day,
                        duration_minutes=random.randint(50, 80),
                        notes=f"Workout on {current_day}"
                    )
                    
                    for item in todays_routine.items.all():
                        ex_name = item.exercise.name
                        if random.random() > 0.7: current_strength[ex_name] += 2.5
                        
                        for _ in range(item.target_sets):
                            WorkoutLog.objects.create(
                                session=session,
                                exercise=item.exercise,
                                weight_used=current_strength[ex_name],
                                reps_achieved=item.target_reps + random.choice([-1, 0, 1])
                            )
                    total_sessions += 1

        self.stdout.write(self.style.SUCCESS(f"Done! Cleaned old data and generated {total_sessions} sessions for Admin."))

    def create_items(self, routine, exercise_tuples, ex_map):
        for name, sets, reps in exercise_tuples:
            RoutineItem.objects.create(
                routine=routine,
                exercise=ex_map[name],
                target_sets=sets,
                target_reps=reps,
                order=1
            )