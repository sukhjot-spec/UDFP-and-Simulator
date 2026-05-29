from dataset_generator import generate_dataset
import time
import config.thermo_config


if __name__ == "__main__":
    print("Simulation started...")
    start = time.time()
    user_DT = float(input("Enter the sampling time difference: "))
    user_time = 30
    batches = int(input("Enter number of Runs: "))

    df = generate_dataset(
        n_batches=batches,
        DT= user_DT,
        total_time= user_time
    )

    print("Simulation finished...")

    filename = f"MF_simulation_DT_{user_DT}.csv"
    df.to_csv(filename, index=False)

    end = time.time()
    print(f'data generated successfully with shape: {df.shape}')
    print(f"execution time: {end-start:.2f} seconds")