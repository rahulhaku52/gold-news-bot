from database import performance_db

def evaluate_active_trades(current_price, current_structure_bias):
    """
    Evaluates active/pending signals for TP/SL hits or reversal invalidation.
    Returns list of trigger update dictionaries.
    """
    active_signals = performance_db.get_active_signals()
    updates = []

    for sig in active_signals:
        sig_id = sig['id']
        direction = sig['direction']
        tp1 = sig['tp1']
        tp2 = sig['tp2']
        tp3 = sig['tp3']
        sl = sig['stop_loss']
        status = sig['status']

        if direction == "BUY":
            # TP Hits
            if current_price >= tp3 and status != 'TP3':
                performance_db.update_signal_status(sig_id, 'TP3')
                updates.append({'type': 'TP3_HIT', 'signal': sig, 'price': current_price})
            elif current_price >= tp2 and status not in ['TP2', 'TP3']:
                performance_db.update_signal_status(sig_id, 'TP2')
                updates.append({'type': 'TP2_HIT', 'signal': sig, 'price': current_price})
            elif current_price >= tp1 and status not in ['TP1', 'TP2', 'TP3']:
                performance_db.update_signal_status(sig_id, 'TP1')
                updates.append({'type': 'TP1_HIT', 'signal': sig, 'price': current_price})

            # SL Hit
            elif current_price <= sl:
                performance_db.update_signal_status(sig_id, 'SL_HIT')
                updates.append({'type': 'SL_HIT', 'signal': sig, 'price': current_price})

            # Reversal / Invalidation
            elif current_structure_bias == "BEARISH":
                performance_db.update_signal_status(sig_id, 'INVALIDATED')
                updates.append({
                    'type': 'REVERSAL_INVALIDATED',
                    'signal': sig,
                    'reason': 'CHoCH Detected / Support Broken',
                    'new_watch': 'SELL Watch Started'
                })

        elif direction == "SELL":
            # TP Hits
            if current_price <= tp3 and status != 'TP3':
                performance_db.update_signal_status(sig_id, 'TP3')
                updates.append({'type': 'TP3_HIT', 'signal': sig, 'price': current_price})
            elif current_price <= tp2 and status not in ['TP2', 'TP3']:
                performance_db.update_signal_status(sig_id, 'TP2')
                updates.append({'type': 'TP2_HIT', 'signal': sig, 'price': current_price})
            elif current_price <= tp1 and status not in ['TP1', 'TP2', 'TP3']:
                performance_db.update_signal_status(sig_id, 'TP1')
                updates.append({'type': 'TP1_HIT', 'signal': sig, 'price': current_price})

            # SL Hit
            elif current_price >= sl:
                performance_db.update_signal_status(sig_id, 'SL_HIT')
                updates.append({'type': 'SL_HIT', 'signal': sig, 'price': current_price})

            # Reversal / Invalidation
            elif current_structure_bias == "BULLISH":
                performance_db.update_signal_status(sig_id, 'INVALIDATED')
                updates.append({
                    'type': 'REVERSAL_INVALIDATED',
                    'signal': sig,
                    'reason': 'CHoCH Detected / Resistance Broken',
                    'new_watch': 'BUY Watch Started'
                })

    return updates

if __name__ == '__main__':
    print("Reversal detector module ready.")
