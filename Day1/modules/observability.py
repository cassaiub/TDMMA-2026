import pandas as pd
from alerce.core import Alerce
import os
import math

# Initialize the global ALeRCE client for backend validation
alerce_client = Alerce()

def cassa_tns_check(oid: str, ra: float, dec: float, use_live_api: bool = True) -> bool:
    """
    Validates a candidate ZTF object against the Mock Transient Name Server (TNS).
    Acts as a pedagogical grading engine by evaluating the historical baseline.

    Parameters:
        oid (str): The ZTF Object ID.
        ra (float): Right Ascension (used for payload completeness check).
        dec (float): Declination (used for payload completeness check).
        use_live_api (bool): If True, queries ALeRCE directly. If False, checks the parquet file.

    Returns:
        bool: True if approved (UNCLASSIFIED), False if rejected (AGN/Imposter).
    """
    print(f"[*] Transmitting OID {oid} to CASSA Cross-Match Engine...")
    
    baseline_days = 0.0

    if use_live_api:
        try:
            stats = alerce_client.query_magstats(oid)
            df_stats = pd.DataFrame(stats)

            if df_stats.empty:
                print(f"[\033[91mAPI ERROR\033[0m] OID {oid} returned no photometric statistics.")
                return False

            first_mjd = df_stats['firstmjd'].min()
            last_mjd = df_stats['lastmjd'].max()
            baseline_days = last_mjd - first_mjd

        except Exception as e:
            print(f"[\033[91mCONNECTION ERROR\033[0m] TNS server unreachable: {e}")
            return False
            
    else:
        parquet_path = os.path.join("data", "reference_alerts.parquet")
        
        if not os.path.exists(parquet_path):
            parquet_path = os.path.join("..", "data", "reference_alerts.parquet")

        try:
            df_offline = pd.read_parquet(parquet_path)
            target = df_offline[df_offline['oid'] == oid]

            if target.empty:
                print(f"[\033[91mERROR\033[0m] OID {oid} not found in offline data stream.")
                return False

            first_mjd = target['firstmjd'].values[0]
            last_mjd = target['lastmjd'].values[0]
            baseline_days = last_mjd - first_mjd

        except Exception as e:
            print(f"[\033[91mI/O ERROR\033[0m] Failed to parse local Failsafe Database: {e}")
            return False

    if baseline_days > 100:
        print(f"[\033[91mREJECTED\033[0m] Cross-match found in TNS/SIMBAD archives.")
        print(f"    -> Historical photometric baseline detected: {baseline_days:.1f} days.")
        print(f"    -> Classification: Active Galactic Nucleus (AGN) or Long-Period Variable.")
        print(f"    -> \033[91mACTION:\033[0m Do not observe. Select a different candidate.\n")
        return False
    else:
        print(f"[\033[92mAPPROVED\033[0m] No matches found in global catalogs.")
        print(f"    -> Historical photometric baseline detected: {baseline_days:.1f} days.")
        print(f"    -> Classification: UNCLASSIFIED Transient.")
        print(f"    -> \033[92mACTION:\033[0m Target verified. Proceed to LCO Payload Generation.\n")
        return True


def submit_lco_trigger(payload: dict) -> bool:
    """
    Mock LCO Observation Portal API. 
    Validates a JSON-like payload for telescope integrity, observability, and exposure physics.
    """
    print("Initiating LCO Observation Portal API Handshake...")

    try:
        target = payload["Target"]
        constraints = payload["Constraints"]
        instrument = payload["Instrument"]
        
        name = target["Name"]
        ra = float(target["RA"])
        dec = float(target["Dec"])
        mag = float(target["Magnitude"])
        
        req_airmass = float(constraints["Max_Airmass"])
        req_snr = float(constraints["Required_SNR"])
        
        req_time = float(instrument["Exposure_Time"])
        telescope = instrument["Telescope"]
        spectrograph = instrument["Spectrograph"]
        
    except KeyError as e:
        print(f"\n[\033[91m400 BAD REQUEST\033[0m] Malformed JSON Payload.")
        print(f"Missing required key: {e}")
        return False
    except (ValueError, TypeError):
        print(f"\n[\033[91m400 BAD REQUEST\033[0m] Data Type Error.")
        print("Ensure coordinates, magnitude, SNR, and exposure time are numerical values.")
        return False

    # Cerro Tololo Inter-American Observatory (CTIO) Latitude
    ctio_lat = -30.169 
    
    zenith_angle_deg = abs(ctio_lat - dec)
    
    if zenith_angle_deg >= 90:
        print("\n[\033[91m403 FORBIDDEN\033[0m] Observability constraint failed.")
        print("Target is strictly below the horizon at Cerro Tololo.")
        return False
        
    min_airmass = 1.0 / math.cos(math.radians(zenith_angle_deg))
    
    if min_airmass > req_airmass or min_airmass > 1.5:
        print(f"\n[\033[91m409 CONFLICT\033[0m] Observability constraint failed.")
        print(f"Target's minimum airmass from Chile is {min_airmass:.2f}. Cannot satisfy Max_Airmass <= 1.5.")
        return False

    t_0 = 300.0
    m_0 = 18.0
    snr_0 = 10.0
    
    mag_scaling = 10 ** (0.4 * (mag - m_0))
    snr_scaling = (req_snr / snr_0) ** 2
    required_t_exp = t_0 * mag_scaling * snr_scaling
    
    if req_time < (0.8 * required_t_exp):
        print(f"\n[\033[91m422 UNPROCESSABLE ENTITY\033[0m] Exposure time mathematically insufficient.")
        print(f"Target will be lost in background noise. Recalculate your exposure time.")
        return False

    if req_time > 1800:
        print(f"\n[\033[91m402 PAYMENT REQUIRED\033[0m] Allocation Exceeded.")
        print(f"Requested {req_time}s. Dr. Ashraf's ToO limits you to 30 minutes (1800s).")
        return False
        
    if telescope.lower() != "2-meter" or spectrograph.upper() != "FLOYDS":
        print(f"\n[\033[91m404 NOT FOUND\033[0m] Instrument configuration unrecognized.")
        print("Ensure you are requesting the '2-meter' telescope and 'FLOYDS' spectrograph.")
        return False

    print("\n[\033[92m200 OK\033[0m] Payload accepted by LCO Observation Portal.")
    print("[\033[94mINFO\033[0m] Calculating ephemerides and scheduling observation on 2m0a (Cerro Tololo).")
    print("[\033[92mSUCCESS\033[0m] Telescope slewing to target. Dome opening...")
    print(f"      -> Target: {name}")
    print(f"      -> Expected SNR: ~{req_snr} in {req_time} seconds.")
    
    return True